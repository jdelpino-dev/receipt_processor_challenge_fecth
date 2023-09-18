# Step 5: Define the Receipt model
class Receipt(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID as the primary key
    retailer = db.Column(db.String(255), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_time = db.Column(db.Time, nullable=False)
    total = db.Column(db.Float, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __init__(self, id, retailer, purchase_date, purchase_time, total, points):
        self.id = id
        self.retailer = retailer
        self.purchase_date = purchase_date
        self.purchase_time = purchase_time
        self.total = total
        self.points = points
