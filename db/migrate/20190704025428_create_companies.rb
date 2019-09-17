class CreateCompanies < ActiveRecord::Migration[5.1]
  def change
    create_table :companies do |t|
      t.string :name, null: false
      t.integer :reputation, null: false
      t.string :image
      t.references :business, foreign_key: true, null: false
      t.string :description

      t.index :name, unique: true

      t.timestamps
    end
  end
end
