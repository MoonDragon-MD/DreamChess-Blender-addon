import bpy
import bmesh
import os
import subprocess
from collections import defaultdict

def triangulate_mesh(obj):
    """Triangola la mesh dell'oggetto attivo."""
    print(f"Triangolazione della mesh: {obj.name}")
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    triangulated_mesh = bpy.data.meshes.new(name=f"{obj.data.name}_triangulated")
    bm.to_mesh(triangulated_mesh)
    bm.free()
    return triangulated_mesh

# Funzione per trovare i triangoli adiacenti
def get_adjacent_triangles(mesh):
    edge_to_faces = defaultdict(list)
    for face in mesh.polygons:
        for edge_key in face.edge_keys:
            edge_to_faces[edge_key].append(face.index)
    adjacent = {face.index: [] for face in mesh.polygons}
    for faces in edge_to_faces.values():
        if len(faces) == 2:  # Due triangoli condividono un lato
            adjacent[faces[0]].append(faces[1])
            adjacent[faces[1]].append(faces[0])
    return adjacent

# Ordinamento con DFS
def dfs_order(start, adjacent, visited):
    order = []
    stack = [start]
    while stack:
        face = stack.pop()
        if face not in visited:
            visited.add(face)
            order.append(face)
            for adj in adjacent[face]:
                if adj not in visited:
                    stack.append(adj)
    return order

# Ottieni l'ordine dei triangoli
def get_ordered_triangles(mesh):
    adjacent = get_adjacent_triangles(mesh)
    visited = set()
    order = []
    for face in range(len(mesh.polygons)):
        if face not in visited:
            order.extend(dfs_order(face, adjacent, visited))
    return order

def write(filepath, context):
    """Esporta la mesh attiva in formato DCM per DreamChess."""
    print("Inizio esportazione verso:", filepath)
    
    # Verifica che ci sia un oggetto mesh attivo
    obj = context.view_layer.objects.active
    if not obj or obj.type != 'MESH':
        raise ValueError("Nessun oggetto mesh attivo selezionato")

    # Triangola la mesh
    triangulated_mesh = triangulate_mesh(obj)
    temp_file = filepath + ".0000"  # File temporaneo in formato "0000"
    print("Scrittura del file temporaneo:", temp_file)

    # Ottieni l'ordine dei triangoli
    ordered_faces = get_ordered_triangles(triangulated_mesh)

    # Apertura e scrittura del file DCM
    with open(temp_file, "w") as file:
        file.write("DCM 0000\n")
        
        # Scrittura dei vertici con coordinate e normali
        file.write(f"{len(triangulated_mesh.vertices)}\n")
        for vertex in triangulated_mesh.vertices:
            co = vertex.co  # Coordinate
            norm = vertex.normal  # Normali
            file.write(f"{co.x:.6f} {co.y:.6f} {co.z:.6f} {norm.x:.6f} {norm.y:.6f} {norm.z:.6f}\n")
        
        # Scrittura delle facce con indici e UV in ordine ottimizzato
        file.write(f"{len(triangulated_mesh.polygons)}\n")
        uv_layer = triangulated_mesh.uv_layers.active
        if uv_layer is None:
            print("Nessuna mappa UV trovata, uso UV predefinite")
            for face_index in ordered_faces:
                poly = triangulated_mesh.polygons[face_index]
                v = poly.vertices
                # Ordine invertito per correggere il winding
                file.write(f"{v[2] + 1} {v[1] + 1} {v[0] + 1} 0 0 0.5 0.5 1 1\n")
        else:
            for face_index in ordered_faces:
                poly = triangulated_mesh.polygons[face_index]
                loop_indices = poly.loop_indices
                # Estrazione degli indici dei vertici dai loop
                v0 = triangulated_mesh.loops[loop_indices[0]].vertex_index
                v1 = triangulated_mesh.loops[loop_indices[1]].vertex_index
                v2 = triangulated_mesh.loops[loop_indices[2]].vertex_index
                # Estrazione delle coordinate UV
                uv0 = uv_layer.data[loop_indices[0]].uv
                uv1 = uv_layer.data[loop_indices[1]].uv
                uv2 = uv_layer.data[loop_indices[2]].uv
                # Scrittura con ordine invertito per correggere il winding
                file.write(f"{v2 + 1} {v1 + 1} {v0 + 1} {uv2.x:.6f} {uv2.y:.6f} {uv1.x:.6f} {uv1.y:.6f} {uv0.x:.6f} {uv0.y:.6f}\n")

    # Conversione con dcmstrip
    print("File temporaneo scritto, chiamata all'eseguibile dcmstrip")
    try:
        dcmstrip_path = os.path.join(os.path.dirname(__file__), "dcmstrip")
        cache_size = "2048"  # Valore di cache_size come stringa
        subprocess.run([dcmstrip_path, temp_file, filepath, cache_size], check=True)
        print("Conversione completata con successo!")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante la conversione: {e}")
        raise
    except FileNotFoundError:
        print("Errore: eseguibile 'dcmstrip' non trovato. Assicurati che sia nella directory dell'addon.")
        raise

    # Pulizia
    os.remove(temp_file)
    bpy.data.meshes.remove(triangulated_mesh)
    print("Esportazione completata con successo")
    return "Esportazione completata: " + filepath

# Esempio di utilizzo (opzionale, per test diretto in Blender)
if __name__ == "__main__":
    write("/percorso/del/tuo/file.dcm", bpy.context)