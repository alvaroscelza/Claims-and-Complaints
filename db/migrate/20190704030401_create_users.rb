class CreateUsers < ActiveRecord::Migration[5.1]
  def change
    create_table :users do |t|
      t.string :name
      t.integer :reputation
      t.string :password
      t.string :email
      t.string :image
      t.Role :role
      t.[Permit] :permits

      t.timestamps
    end
  end
end
