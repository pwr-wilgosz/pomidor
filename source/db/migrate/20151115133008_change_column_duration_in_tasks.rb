class ChangeColumnDurationInTasks < ActiveRecord::Migration
  def change
    remove_column :tasks, :duration, :datetime
    add_column :tasks, :duration, :integer
  end
end
