class AddCommentToRimsAndHubs < ActiveRecord::Migration
  def self.up
    add_column :rims, :comment, :string
    add_column :hubs, :comment, :string
  end

  def self.down
    remove_column :rims, :comment
    remove_column :hubs, :comment
  end
end
