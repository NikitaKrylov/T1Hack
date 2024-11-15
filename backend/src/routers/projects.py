from fastapi import APIRouter

router = APIRouter(
    tags=['Main'],
    prefix="/projects",
)


@router.post('')
async def create_project():
    pass


@router.get('/{project_id}')
async def get_project_info(project_id: int):
    pass


@router.patch('/{project_id}')
async def update_project_info(project_id: int):
    pass


@router.delete('/{project_id}')
async def delete_project(project_id: int):
    pass


@router.get('/{project_id}/contributors')
async def get_project_contributors(project_id: int):
    pass


@router.put('/{project_id}/contributors')
async def add_contributors(project_id: int, new_contributors: list[int]):
    pass


@router.delete('/{project_id}/contributors/{contributor_id}')
async def remove_contributor(project_id: int, contributor_id: int):
    pass




