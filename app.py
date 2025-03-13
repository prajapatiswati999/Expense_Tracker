from flask import Flask, render_template, request, redirect, url_for
import logging

def create_app():
    app = Flask(__name__)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # In-memory storage for transactions and balance
    transactions = []
    balance = 0

    @app.route('/')
    def index():
        logging.info("Rendering index page.")
        return render_template('index.html', balance=balance, transactions=transactions)

    @app.route('/add_transaction', methods=['POST'])
    def add_transaction():
        try:
            amount = float(request.form['amount'])
            transaction_type = request.form['type']
            logging.info(f"Received transaction: Amount={amount}, Type={transaction_type}")

            # Update balance based on transaction type
            nonlocal balance
            if transaction_type == 'income':
                balance += amount
            elif transaction_type == 'expense':
                balance -= amount

            # Store transaction
            transactions.append({'amount': amount, 'type': transaction_type})

            logging.info(f"Updated balance: {balance}")

            # Redirect to index page after form submission
            return redirect(url_for('index'))
        except Exception as e:
            logging.error("Error processing transaction", exc_info=True)
            return "An error occurred while processing the transaction.", 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)