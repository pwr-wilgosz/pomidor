class TasksController < ApplicationController
  load_resource :list
  load_and_authorize_resource :task, through: :list

  respond_to :html

  def index
    @tasks = @list.tasks.all

    respond_to do |format|
      format.html
      format.json { render json: { tasks_count: @list.tasks.count, tasks: @tasks } }
    end
  end

  def show
    respond_with(@task)
  end

  def new
    @task = @list.tasks.new
    respond_with(@task)
  end

  def edit
  end

  def create
    @task = @list.tasks.new(task_params)
    @task.save
    respond_with(@task, location: @list)
  end

  def update
    @task.update(task_params)
    respond_with(@task, location: @list)
  end

  def destroy
    @task.destroy
    respond_with(@list)
  end

  private

  def task_params
    params.require(:task).permit(:name, :list_id, :duration, :priority, :x, :y)
  end
end
