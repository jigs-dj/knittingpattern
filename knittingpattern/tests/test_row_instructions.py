from pytest import fixture
from .test_example_rows import a1, charlotte


@fixture
def row0(a1):
    return a1.rows.at(0)


@fixture
def row1(a1):
    return a1.rows.at(1)


@fixture
def row2(a1):
    return a1.rows.at(2)

    
@fixture
def mesh0(row0):
    return row0.produced_meshes[0]


@fixture
def instruction0(row0):
    return row0.instructions[0]


@fixture
def instruction1(row1):
    return row1.instructions[0]


def test_row0_consumes_empty_meshes(row0):
    assert len(row0.consumed_meshes) == 5
    assert all(mesh.is_empty() for mesh in row0.consumed_meshes)


def test_row0_produces_5_meshes(row0):
    assert len(row0.produced_meshes) == 5
    assert all(mesh.does_knit() for mesh in row0.produced_meshes)


def test_row0_meshes_point_also_to_row1(mesh0, row0, row1):
    assert mesh0.produced_in_row == row0
    assert mesh0.consumed_in_row == row1


def test_row0_instruction_produces_mesh_0(mesh0, instruction0):
    assert instruction0 == mesh0.instruction_produced_by
    assert instruction0.produced_meshes == [mesh0]
    assert instruction0.number_of_produced_meshes == 1


def test_instruction0_is_knit(instruction0):
    assert instruction0.does_knit()


def test_instruction_position_in_row(row0, instruction0):
    assert instruction0.row == row0
    assert instruction0.index_in_row_instructions == 0
    assert row0.instructions[0] == instruction0


def test_mesh0_is_consumed_by_instruction1(mesh0, instruction1):
    assert mesh0.instruction_consumed_by == instruction1
    assert instruction1.consumed_meshes == [mesh0]


def test_instruction1_is_knit(instruction1):
    assert instruction1.is_knit()


def test_instruction1_position_in_row(instruction1):
    assert instruction1.position_in_row == 0


def test_mesh0_is_produced(mesh0):
    assert mesh0.is_produced()
    assert mesh0.is_consumed()

def test_instruction0_builds_on_unproduced_meshes(instruction0):
    assert not instruction0.consumed_meshes[0].is_produced()
    
@fixture
def skp(row2):
    return row2.instructions[0]


@fixture
def yo(row2):
    return row2.instructions[1]


def test_yarn_over(yo):
    assert yo.number_of_consumed_meshes == 0
    assert yo.number_of_produced_meshes == 1


def test_skp(skp):
    assert skp.number_of_consumed_meshes == 2
    assert skp.number_of_produced_meshes == 1


def test_position_in_row2(skp, yo, row2):
    assert skp.row == row2
    assert yo.row == row2
    assert skp.index_in_row_instructions == 0
    assert yo.index_in_row_instructions == 1


def test_skp_consumed_meshes_from_row1(skp, row1, row2):
    assert len(skp.produced_meshes) == 1
    assert len(skp.consumed_meshes) == 2
    m1, m2 = skp.consumed_meshes
    assert m1.consumed_by_instruction == skp
    assert m1.consumed_by_row == row2
    assert m1.produced_in_row == row1
    assert m1.mesh_index_in_producing_row == 1
    assert m1.is_produced()
    assert m1.is_consumed()
    assert m2.consumed_by_instruction == skp
    assert m2.consumed_by_row == row2
    assert m2.produced_in_row == row1
    assert m2.mesh_index_in_producing_row == 2
    assert m2.mesh_index_in_consuming_row == 2


def test_skp_produces_one_mesh(skp):
    assert len(skp.produced_meshes) == 1


def test_skp_produced_meshes(skp, row2):
    m = skp.produced_meshes[0]
    assert m.produced_by_instruction == skp
    assert m.is_produced()
    assert not m.is_consumed()
    assert m.mesh_index_in_producing_row == 1
    assert m.produced_by_row == row2


def test_yarn_over_consumes_no_meshes(yo):
    assert yo.consumed_meshes == []


def test_yarn_over_produces_a_mesh(yo):
    assert len(yo.produced_meshes) == 1
    m = yo.produced_meshes[0]
    assert m.produced_by_instruction == yo
    assert m.produced_in_row == yo.row
    assert m.mesh_index_in_producing_row == 1
