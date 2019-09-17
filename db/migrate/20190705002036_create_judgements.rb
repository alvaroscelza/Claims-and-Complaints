class CreateJudgements < ActiveRecord::Migration[5.1]
  def change
    create_table :judgements do |t|
      t.string :opinion, null: false
      t.boolean :vote, null: false
      t.references :user, null: false
      t.references :company, null: false

      t.timestamps
    end
  end
end
