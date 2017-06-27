from flask import *
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
from sqlalchemy import *

#Initialize Flask with name of the python application
app = Flask(__name__)

#SQLAlchemy Initialization
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/restaurants')
def restaurants():

    restaurants = session.query(Restaurant).all()

    return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()

    return render_template('menu.html',restaurant = restaurant, items = menuItems)

@app.route('/restaurants/<int:restaurant_id>/new',methods=['GET','POST'])
def addMenuItem(restaurant_id):

    if request.method == 'POST':
        newMenuItem = MenuItem(name = request.form['name'],restaurant_id = restaurant_id,price=request.form['price'],description=request.form['description'])
        session.add(newMenuItem)
        session.commit()
        flash(newMenuItem.name + " was added to the Menu")
        #Return a url_redirect to the MenuItemPage
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

    else :
        #Render template here
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newMenuItem.html',restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):

    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    oldName = menuItem.name
    if request.method == 'POST':
        menuItem.name = request.form['name']
        session.add(menuItem)
        session.commit()
        flash(oldName + " was modified to " + request.form['name'])
        #Return a url_redirect to the MenuItemPage
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

    else :
        #Render template here
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editMenuItem.html',restaurant = restaurant,menuItem = menuItem)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    oldName = menuItem.name
    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash(oldName + " was deleted from the menu")

        # Return a url_redirect to the MenuItemPage
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        # Render template here
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('deleteMenuItem.html', restaurant=restaurant, menuItem=menuItem)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    return jsonify(MenuItem = item.serialize)


#Server is run only if ran directly
#Not executed if imported
if __name__ == '__main__':

    app.secret_key = 'my_secret_key'
    #Server reload automatically if code is changed
    app.debug = True
    #Make server publically available as we are using a vagrant environment
    app.run(host='0.0.0.0',port=5000)
