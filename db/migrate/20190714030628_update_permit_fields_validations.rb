class UpdatePermitFieldsValidations < ActiveRecord::Migration[5.1]
  def change
    change_column :permits, :name, :string, null: false
    change_column :permits, :needed_reputation, :integer, null: false
    add_index :permits, :name, unique: true
  end
end
