class WheelController < ApplicationController

  def print
    @no_menu = true
    render :action => "print"
  end

  def update
    
    setup_session

    if @wheel.rim.id != params[:rim].to_i and !params[:rim].nil?
        @rim = Rim.find(params[:rim])

        if !@rim.nil?
          @wheel.rim = @rim
          @rim_list.delete_if{|r| r.has_value?(@rim.id) }
          @rim_list.unshift({@rim.description_for_menu => @rim.id})
          session[:rim_list] = @rim_list
        end
    end


    if @wheel.hub.id != params[:hub].to_i and !params[:hub].nil?
      @hub = Hub.find(params[:hub])

      if !@hub.nil?
        @wheel.hub = @hub
        @hub_list.delete_if{|h| h.has_value?(@hub.id) }
        @hub_list.unshift({@hub.description_for_menu => @hub.id})
        session[:hub_list] = @hub_list
      end
    end
    
    
    @wheel.cross = params[:cross].to_i if !params[:cross].nil?
    @wheel.spokes = params[:spokes].to_i if !params[:spokes].nil?
    @wheel.nipple_correction = params[:nipple_correction].to_i if !params[:nipple_correction].nil?
      
    session[:wheel] = @wheel
  
    if request.xml_http_request?
      render :partial => "layouts/menus", :layout => false
    else
      # redirect_to :controller => "main"
      render :template => "main/index"
    end
  end


end