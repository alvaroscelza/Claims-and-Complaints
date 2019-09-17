class CreatePermits < ActiveRecord::Migration[5.1]
  def change
    create_table :permits do |t|
      t.string :name, null: false
      t.integer :needed_reputation, null: false
      t.index :name, unique: true

      t.timestamps
    end
  end
end
