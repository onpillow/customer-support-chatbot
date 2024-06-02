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
    # Split the date fields into year, month, and day components
    AttributeInfo(
        name="Shipment Date year",
        description="Year when the order was shipped",
        type="integer",
    ),
    AttributeInfo(
        name="Shipment Date month",
        description="Month when the order was shipped",
        type="integer",
    ),
    AttributeInfo(
        name="Shipment Date day",
        description="Day when the order was shipped",
        type="integer",
    ),
    AttributeInfo(
        name="Expected Delivery Date year",
        description="Expected delivery year of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Expected Delivery Date month",
        description="Expected delivery month of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Expected Delivery Date day",
        description="Expected delivery day of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Delivery Date year",
        description="Actual delivery year of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Delivery Date month",
        description="Actual delivery month of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Delivery Date day",
        description="Actual delivery day of the order",
        type="integer",
    ),
    AttributeInfo(
        name="Order Date year",
        description="Year when the order was placed",
        type="integer",
    ),
    AttributeInfo(
        name="Order Date month",
        description="Month when the order was placed",
        type="integer",
    ),
    AttributeInfo(
        name="Order Date day",
        description="Day when the order was placed",
        type="integer",
    ),
    AttributeInfo(
        name="Refund Date year",
        description="Year when the refund was processed",
        type="integer",
    ),
    AttributeInfo(
        name="Refund Date month",
        description="Month when the refund was processed",
        type="integer",
    ),
    AttributeInfo(
        name="Refund Date day",
        description="Day when the refund was processed",
        type="integer",
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
        name="Notification Status",
        description="Indicates whether notifications related to the order are active",
        type="boolean",
    )
]

document_content_description = "Customer order information including order details, customer details, refund information."
