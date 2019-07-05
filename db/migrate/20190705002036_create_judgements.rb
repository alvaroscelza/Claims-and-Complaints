class CreateJudgements < ActiveRecord::Migration[5.1]
  def change
    create_table :judgements do |t|
      t.string :opinion
      t.boolean :vote
      t.reference :user
      t.reference :company

      t.timestamps
    end
  end
end
