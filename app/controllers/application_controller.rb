# Filters added to this controller apply to all controllers in the application.
# Likewise, all the methods added will be available for all controllers.

class ApplicationController < ActionController::Base
  
  def setup_session
    @wheel = session[:wheel] ||= Wheel.new
    @hub_list = session[:hub_list] ||= Array.new
    @rim_list = session[:rim_list] ||= Array.new
  end

  def rescue_action_in_public(exception)
    case(exception)
      when ActiveRecord::RecordNotFound then redirect_to :controller => "main"
    end
  end

end
