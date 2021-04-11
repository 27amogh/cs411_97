""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

# @app.route("/")
# def homepage():
#     return render_template("index.html", name= db_helper.query_name())
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/", methods = ['POST'])
def search():
    checkin = request.form["checkin_date"]
    checkout = request.form["checkout_date"]
    num_guest = request.form["num_guest"]
    listings = db_helper.fetch_listing(checkin, checkout, num_guest)
    return render_template("index.html", data_list = listings)

@app.route("/reviews", methods = ['GET'])
def go_reviews():
    return render_template("reviews.html")

@app.route("/test")
def test():
    return render_template("test.html")



@app.route("/reviews", methods = ['POST'])
def lookup_reviews():
    reviewer_id = request.form['reviewer_id']
    reviewer_name = request.form['reviewer_name']

    result = db_helper.fetch_reviews( reviewer_id, reviewer_name)
    if len(result) == 0:
        return jsonify({'error': 'Wrong reviewer id and reviewer name'})

    return render_template("reviews.html", data_list = result)



@app.route("/reviews/create", methods = ['GET','POST'])
def add_reviews():

    if request.method == 'POST':
        listing_id = request.form['listing_id']
        reviewer_id = request.form['reviewer_id']
        reviewer_name = request.form['reviewer_name']
        comment = request.form['comment']

        result = db_helper.add_reviews(listing_id, reviewer_id, reviewer_name, comment)
        return jsonify({"listing_id": result["listing_id"], "review_id": result["review_id"], "date":result['date'], 
    "reviewer_id": result['reviewer_id'], "reviewer_name": result['reviewer_name'], "comment": result['comment']})

    return render_template("reviews.html")


@app.route("/reviews/update", methods = ['GET','POST'])
def update_reviews():
    print("enter")
    
    comment = request.form.get('new_comment')
    review_id = request.form.get('update_review_id')
    db_helper.update_reviews(review_id,comment)
    print(comment)    
    return jsonify({'success': True, 'response': comment})
        


@app.route("/delete/<int:review_id>", methods=["POST"])
def delete(review_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.delete_reviews(review_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)




# @app.route("/delete/<int:task_id>", methods=['POST'])
# def delete(task_id):
#     """ recieved post requests for entry delete """

#     try:
#         db_helper.remove_task_by_id(task_id)
#         result = {'success': True, 'response': 'Removed task'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


# @app.route("/")
# def homepage():
#     """ returns rendered homepage """
#     items = db_helper.fetch_todo()
#     return render_template("index.html", items=items)