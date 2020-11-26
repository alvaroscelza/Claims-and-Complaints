class CreateJudgements < ActiveRecord::Migration[6.0]
  def change
    create_table :judgements do |t|
      t.string :opinion
      t.boolean :vote
      t.references :user, null: false, foreign_key: true
      t.references :company, null: false, foreign_key: true

      t.timestamps
    end
  end
end
