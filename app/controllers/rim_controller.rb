class RimController < ApplicationController

  def print
    @rims = Rim.find(:all, :order => "size, description")
    @no_menu = true
    render :action => "print"
  end

  def list
    setup_session
    @rims = Rim.search(params[:search], params[:size], params[:page])

    if request.xml_http_request?
      if !params[:search].nil?
        render :partial => "rims_list", :layout => false
      else
        render :partial => "list", :layout => false
      end
    end
  end

  def new
    setup_session
    @rim = Rim.new
    render :partial => "new", :layout => false
  end

  def create
    setup_session
    @rim = Rim.new(params[:rim])
    if @rim.save
      
      Notifier.deliver_rim(@rim)
      
      @rims = Array.new

      @wheel.rim = @rim
      @rim_list.unshift({@rim.description_for_menu => @rim.id})

      session[:wheel] = @wheel
      session[:rim_list] = @rim_list

    	render :update do |page|
        page.replace_html 'top', :partial => 'layouts/menus' 
        page.replace_html 'editor_area', :partial => 'list', :layout => false 
        page.visual_effect :highlight, "results", :duration => 1
        page.visual_effect :highlight, "rim_selector", :duration => 1
      end

    else
      render :update do |page|
        page.replace_html 'editor_area', :partial => 'new', :layout => false 
      end
    end
  end


end
