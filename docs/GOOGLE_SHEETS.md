
## Google Sheets Database Setup

Ensure you have followed the [Google Cloud Setup](/docs/GOOGLE_CLOUD.md) guide, specifically that you have enabled the "Google Sheets API", and have downloaded the service account JSON file into the root directory of this repository and renamed it as "google-credentials.json".

#### Document Setup

Create a new Google Sheet document.

The app will need read and write access to this document.

Modify the document's sharing settings to grant "Edit" privileges to the "client email" address specified in the Google API credentials JSON file (e.g. "my-serice@my-project.iam.gserviceaccount.com").

#### Sheets Setup

Create two example sheets. One called "products" and the other called "orders".

On the "products" sheet, populate the first row with the following column headers:

  + `id`
  + `name`
  + `description`
  + `price`
  + `url`
  + `created_at`

On the "orders" sheet, populate the first row with the following column headers:

  + `id`
  + `user_email`
  + `product_id`
  + `product_name`
  + `product_price`
  + `created_at`


You will notice there are corresponding "model" classes defined in the "app/models" directory. For any sheet, the fields defined in the corresponding model class need to stay consistent with the column names designated in the sheet, except the sheet will have an additional "id" column first and "created_at" column last. For more information, see the [`gspread_models` package docs](https://github.com/s2t2/gspread-models-py).
