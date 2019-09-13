class UpdateBusinessFieldsValidations < ActiveRecord::Migration[5.1]
  def change
    change_column :businesses, :name, :string, null: false
    add_index :businesses, :name, unique: true
  end
end
