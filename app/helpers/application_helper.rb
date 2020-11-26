module ApplicationHelper
  def full_title(page_title = '')
    base_title = 'Claims and Complaints'
    if page_title.empty?
      base_title
    else
      format('%<page_title> | %<base_title>')
    end
  end
end
