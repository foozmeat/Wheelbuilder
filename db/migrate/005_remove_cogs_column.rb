class RemoveCogsColumn < ActiveRecord::Migration
  def self.up
    remove_column :hubs, :cogs
  end

  def self.down
    add_column :hubs, :cogs, :string
  end
end
