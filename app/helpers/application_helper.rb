# Methods added to this helper will be available to all templates in the application.
module ApplicationHelper
  
  def display_age(date)

    return 'Unknown' if date.nil?

    "#{time_ago_in_words(date)}"
  end
  
end
