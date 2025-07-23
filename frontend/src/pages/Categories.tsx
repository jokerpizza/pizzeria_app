import { useEffect, useState } from "react";
import { getCategories, createCategory, updateCategory, deleteCategory } from "../api";

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [newName, setNewName] = useState("");
  const [editId, setEditId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");

  const refresh = async () => {
    setCategories(await getCategories());
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleAdd = async () => {
    if (!newName.trim()) return;
    await createCategory({ name: newName });
    setNewName("");
    refresh();
  };

  const handleEdit = (id: number, name: string) => {
    setEditId(id);
    setEditName(name);
  };

  const handleUpdate = async (id: number) => {
    if (!editName.trim()) return;
    await updateCategory(id, { name: editName });
    setEditId(null);
    refresh();
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Usunąć kategorię?")) {
      await deleteCategory(id);
      refresh();
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Kategorie przepisów</h2>
      <div className="flex mb-4">
        <input
          type="text"
          value={newName}
          onChange={e => setNewName(e.target.value)}
          placeholder="Nowa kategoria"
          className="border p-2 rounded-l w-full"
        />
        <button className="bg-green-500 text-white px-4 rounded-r" onClick={handleAdd}>
          Dodaj
        </button>
      </div>
      <ul>
        {categories.map((cat: any) => (
          <li key={cat.id} className="flex items-center justify-between border-b py-2">
            {editId === cat.id ? (
              <>
                <input
                  type="text"
                  value={editName}
                  onChange={e => setEditName(e.target.value)}
                  className="border p-2 rounded"
                />
                <div>
                  <button
                    className="bg-blue-500 text-white px-2 mx-1 rounded"
                    onClick={() => handleUpdate(cat.id)}
                  >
                    Zapisz
                  </button>
                  <button
                    className="bg-gray-300 px-2 mx-1 rounded"
                    onClick={() => setEditId(null)}
                  >
                    Anuluj
                  </button>
                </div>
              </>
            ) : (
              <>
                <span>{cat.name}</span>
                <div>
                  <button
                    className="bg-yellow-400 text-white px-2 mx-1 rounded"
                    onClick={() => handleEdit(cat.id, cat.name)}
                  >
                    Edytuj
                  </button>
                  <button
                    className="bg-red-500 text-white px-2 mx-1 rounded"
                    onClick={() => handleDelete(cat.id)}
                  >
                    Usuń
                  </button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}