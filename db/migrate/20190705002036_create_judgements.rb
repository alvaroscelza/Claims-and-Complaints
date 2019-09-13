class CreateJudgements < ActiveRecord::Migration[5.1]
  def change
    create_table :judgements do |t|
      t.string :opinion
      t.boolean :vote
      t.references :user
      t.references :company

      t.timestamps
    end
  end
end
