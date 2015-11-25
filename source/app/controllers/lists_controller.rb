class ListsController < ApplicationController
  before_action :edit
  load_and_authorize_resource :list

  def index
    @lists = @lists.where(user_id: current_user.id)
    lists_count = @lists.count
    @lists = @lists.page(current_page).per(per_page)
    respond_to do |format|
      format.html
      format.json { render json: { lists_count: lists_count, lists: @lists } }
    end
  end

  def show
    @q1_tasks = @list.tasks.quarter1
    @q2_tasks = @list.tasks.quarter2
    @q3_tasks = @list.tasks.quarter3
    @q4_tasks = @list.tasks.quarter4
    respond_to do |format|
      format.html
      format.json { render json: @list }
    end
  end

  def new
    @list = List.new
  end

  def edit
  end

  def create
    @list = current_user.lists.create(list_params)

    respond_with @list, serializer: ListSerializer
  end

  def update
    @list.update_attributes(list_params)

    respond_with @list, serializer: ListSerializer
  end

  def destroy
    @list.destroy
    redirect_to lists_path
  end

  private

  def list_params
    params.require(:list).permit(:name)
  end
end
