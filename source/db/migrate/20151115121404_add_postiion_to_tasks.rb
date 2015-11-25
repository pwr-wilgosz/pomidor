class AddPostiionToTasks < ActiveRecord::Migration
  def change
    add_column :tasks, :x, :integer
    add_column :tasks, :y, :integer
  end
end
