require "application_system_test_case"

class JudgementsTest < ApplicationSystemTestCase
  setup do
    @judgement = judgements(:one)
  end

  test "visiting the index" do
    visit judgements_url
    assert_selector "h1", text: "Judgements"
  end

  test "creating a Judgement" do
    visit judgements_url
    click_on "New Judgement"

    fill_in "Company", with: @judgement.company_id
    fill_in "Opinion", with: @judgement.opinion
    fill_in "User", with: @judgement.user_id
    check "Vote" if @judgement.vote
    click_on "Create Judgement"

    assert_text "Judgement was successfully created"
    click_on "Back"
  end

  test "updating a Judgement" do
    visit judgements_url
    click_on "Edit", match: :first

    fill_in "Company", with: @judgement.company_id
    fill_in "Opinion", with: @judgement.opinion
    fill_in "User", with: @judgement.user_id
    check "Vote" if @judgement.vote
    click_on "Update Judgement"

    assert_text "Judgement was successfully updated"
    click_on "Back"
  end

  test "destroying a Judgement" do
    visit judgements_url
    page.accept_confirm do
      click_on "Destroy", match: :first
    end

    assert_text "Judgement was successfully destroyed"
  end
end
