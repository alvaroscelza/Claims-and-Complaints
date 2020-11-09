class CreateSuggestions < ActiveRecord::Migration[6.0]
  def change
    create_table :suggestions do |t|
      t.datetime :date_time
      t.text :description
      t.references :user, null: false, foreign_key: true

      t.timestamps
    end
  end
end
