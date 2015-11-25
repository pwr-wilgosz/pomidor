class Task < ActiveRecord::Base
  belongs_to :list

  include WithIdentifier

  REQUIRED_TASK_PARAMS = [:name, :updated_at, :identifier]
  OPTIONAL_TASK_PARAMS = [:x, :y, :duration, :priority]
  ALL_TASK_PARAMS = REQUIRED_TASK_PARAMS | OPTIONAL_TASK_PARAMS

  PRIORITIES = (1..4).to_a
  QUARTER_SIZE = { x: 500, y: 500 }

  QUARTER_1 = {
                x: { min: 1, max: QUARTER_SIZE[:x] },
                y: { min: 1, max: QUARTER_SIZE[:y] }
              }
  QUARTER_2 = {
                x: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:x] },
                y: { min: 1, max: QUARTER_SIZE[:y] }
              }
  QUARTER_3 = {
                x: { min: 1, max: QUARTER_SIZE[:x] },
                y: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:y] }
              }
  QUARTER_4 = {
                x: { min: QUARTER_SIZE[:x]+1, max: 2*QUARTER_SIZE[:x] },
                y: { min: QUARTER_SIZE[:y]+1, max: 2*QUARTER_SIZE[:y] }
              }

  scope :quarter1, ->{ where(priority: 1) }
  scope :quarter2, ->{ where(priority: 2) }
  scope :quarter3, ->{ where(priority: 3) }
  scope :quarter4, ->{ where(priority: 4) }


  after_initialize :set_position
  AVAILABLE_LABELS = ["Default", "Primary", "Success", "Info", "Warning", "Danger"]

  def self.random_label
    AVAILABLE_LABELS[rand(AVAILABLE_LABELS.length)].downcase
  end

  private

  def set_position
    self.duration ||= rand(4)+1
    self.priority ||= rand(PRIORITIES.length)+1
    self.x ||= rand(QUARTER_SIZE[:x])
    self.y ||= rand(QUARTER_SIZE[:y])
  end

  class << self

    def valid_task(task_params)
      (REQUIRED_TASK_PARAMS - task_params.keys).empty?
    end

    def update_task task, task_params
      if task.updated_at < task_params[:updated_at]
        task.update_attributes(task_params.slice(*ALL_TASK_PARAMS))
      end
    end


    def sync list, tasks
      tasks.each do |task_params|
        task_params.stringify_keys!

        if valid_task(task_params)
          if (task = list.tasks.find_by(identifier: task_params[:identifier])).present?

          update_task(task, task_params)

          else
            list.create_list(task_params.slice(*REQUIRED_TASK_PARAMS))
          end
        end
      end
    end
  end
end
