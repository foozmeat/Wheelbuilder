class AddEmailToRimAndHub < ActiveRecord::Migration
  def self.up
    add_column :rims, :email, :string
    add_column :hubs, :email, :string    
  end

  def self.down
    remove_column :rims, :email
    remove_column :hubs, :email    
  end
end
