
@app.route('/add_cost', methods=['GET', 'POST'])
@login_required
@role_required('add_cost')
def add_cost():
    if request.method == 'POST':
        cost_date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'] or 0)
        payment_method = request.form['payment_method']

        new_cost = Cost(
            date=cost_date,
            category=category,
            description=description,
            amount=amount,
            payment_method=payment_method
        )
        db.session.add(new_cost)
        db.session.commit()

        return redirect(url_for('costs_list'))

    return render_template('add_cost.html', categories=global_categories)
