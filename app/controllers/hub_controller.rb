class HubController < ApplicationController

  def index
    list
    render :action => "list"
  end

  def print
    @hubs = Hub.find(:all, :order => "forr,description")
    @no_menu = true
    render :action => "print"
  end

  def list
    setup_session
    @hubs = Hub.search(params[:search], params[:forr], params[:page])

    if request.xml_http_request?
      if !params[:search].nil?
        render :partial => "hubs_list", :layout => false
      else
        render :partial => "list", :layout => false
      end
    end

  end

  def new
    setup_session
    @hub = Hub.new
    render :partial => "new", :layout => false
  end

  def create
    setup_session
    @hub = Hub.new(params[:hub])
    if @hub.save
      Notifier.deliver_hub(@hub)
      
      @hubs = Array.new

      @wheel.hub = @hub
      @hub_list.unshift({@hub.description_for_menu => @hub.id})

      session[:wheel] = @wheel
      session[:hub_list] = @hub_list
      
    	render :update do |page|
        page.replace_html 'top', :partial => 'layouts/menus' 
        page.replace_html 'editor_area', :partial => 'list', :layout => false 
        page.visual_effect :highlight, "results", :duration => 1
        page.visual_effect :highlight, "hub_selector", :duration => 1
      end
      
    else
      render :update do |page|
        page.replace_html 'editor_area', :partial => 'new', :layout => false 
      end
    end
  end

end
