class AddWidthToRim < ActiveRecord::Migration
  def self.up
    add_column :rims, :width, :integer
  end

  def self.down
    remove_column :rims, :width
  end
end
