class ListsController < ApplicationController
  # before_filter :restrict_access, only: [:create, :update]

  def index
    if params[:per_page].present? && params[:page].present?
      offset = params[:per_page].to_i * (params[:page].to_i - 1)
    else
      params[:per_page] = 10
      params[:page] = 0
    end
    @lists = List.all.order(created_at: :desc).offset(offset).limit(params[:per_page].to_i)

    respond_with @lists, each_serializer: ListSerializer
  end

  def show
    @list = List.find(params[:id])

    respond_with @list, serializer: ListSerializer
  end

  def create
    @list = List.create(list_params)
    # @list.update_attributes(user_id: ApiKey.find_by_access_token(params[:access_token]).user.id)

    respond_with @list, serializer: ListSerializer
  end

  def update
    @list = List.find(params[:id]).update(title: params[:title])

    respond_with @list, serializer: ListSerializer
  end

  private

  def list_params
    params.require(:list).permit(:name)
  end

  def restrict_access
    # api_key = ApiKey.find_by_access_token(params[:access_token])

    # if params[:id].present?
    #   head :unauthorized unless api_key && List.find(params[:id]).user.api_key.access_token == params[:access_token]
    # else
    #   head :unauthorized unless api_key
    # end
  end
end
