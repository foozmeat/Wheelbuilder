class AddTimestamps < ActiveRecord::Migration
  def self.up
    add_column :rims, :created_on, :timestamp
    add_column :hubs, :created_on, :timestamp
    add_column :rims, :updated_on, :timestamp
    add_column :hubs, :updated_on, :timestamp
  end

  def self.down
    remove_column :rims, :created_on
    remove_column :hubs, :created_on
    remove_column :rims, :updated_on
    remove_column :hubs, :updated_on
  end
end
