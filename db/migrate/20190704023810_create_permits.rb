class CreatePermits < ActiveRecord::Migration[5.1]
  def change
    create_table :permits do |t|
      t.string :name
      t.integer :needed_reputation

      t.timestamps
    end
  end
end
