class CreateUsers < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string :name
      t.integer :reputation
      t.string :password
      t.string :email
      t.string :image
      t.references :role, foreign_key: true
      t.references :permits, foreign_key: true

      t.timestamps
    end
  end
end
