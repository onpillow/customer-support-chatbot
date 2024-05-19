from langchain.chains.query_constructor.base import AttributeInfo

metadata_field_info = [
    AttributeInfo(
        name="Order ID",
        description="Unique identifier for each order",
        type="string",
    ),
    AttributeInfo(
        name="Tracking Number",
        description="Tracking number associated with the shipment of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Shipment Date",
        description="The date on which the order was shipped",
        type="date",
    ),
    AttributeInfo(
        name="Expected Delivery Date",
        description="The estimated date on which the order is expected to be delivered",
        type="date",
    ),
    AttributeInfo(
        name="Delivery Date",
        description="The actual date on which the order was delivered",
        type="date",
    ),
    AttributeInfo(
        name="Status",
        description="Current status of the order (e.g., pending, delivered, cancelled)",
        type="string",
    ),
    AttributeInfo(
        name="Customer ID",
        description="Unique identifier for the customer who placed the order",
        type="string",
    ),
    AttributeInfo(
        name="Customer Name",
        description="Name of the customer who placed the order",
        type="string",
    ),
    AttributeInfo(
        name="Customer Email",
        description="Email address of the customer",
        type="string",
    ),
    AttributeInfo(
        name="Customer Phone",
        description="Phone number of the customer",
        type="string",
    ),
    AttributeInfo(
        name="Order Date",
        description="The date on which the order was placed",
        type="date",
    ),
    AttributeInfo(
        name="Refund Requested",
        description="Indicates whether a refund was requested for the order",
        type="boolean",
    ),
    AttributeInfo(
        name="Refund Reason",
        description="The reason provided by the customer for requesting a refund",
        type="string",
    ),
    AttributeInfo(
        name="Refund Status",
        description="Current status of the refund request (e.g., approved, rejected)",
        type="string",
    ),
    AttributeInfo(
        name="Refund Date",
        description="The date on which the refund was processed",
        type="date",
    ),
    AttributeInfo(
        name="Notification Status",
        description="Indicates whether notifications related to the order are active",
        type="boolean",
    )
]
document_content_description = "Customer order information including order details, customer details, refund information."
