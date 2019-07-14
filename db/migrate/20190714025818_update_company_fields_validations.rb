class UpdateCompanyFieldsValidations < ActiveRecord::Migration[5.1]
  def change
    change_column :companies, :name, :string, null: false
    change_column :companies, :reputation, :integer, null: false
    change_column :companies, :business_id, :integer, null: false
    add_index :companies, :name, unique: true
  end
end
