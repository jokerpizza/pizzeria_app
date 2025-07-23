import { useEffect, useState } from "react";
import { getRecipes, createRecipe, getCategories } from "../api";

export default function Recipes() {
  const [recipes, setRecipes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filter, setFilter] = useState<number | null>(null);
  const [name, setName] = useState("");
  const [categoryId, setCategoryId] = useState<number | "">("");

  useEffect(() => {
    refresh();
    getCategories().then(setCategories);
  }, []);

  const refresh = async () => {
    setRecipes(await getRecipes());
  };

  const filtered = filter
    ? recipes.filter((r: any) => r.category_id === filter)
    : recipes;

  const handleAdd = async () => {
    if (!name || !categoryId) return;
    await createRecipe({ name, category_id: categoryId });
    setName("");
    setCategoryId("");
    refresh();
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Przepisy</h2>

      <div className="flex items-center mb-4">
        <select
          className="border p-2 rounded mr-2"
          value={filter ?? ""}
          onChange={e => setFilter(e.target.value ? Number(e.target.value) : null)}
        >
          <option value="">-- wszystkie kategorie --</option>
          {categories.map((cat: any) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
        <button className="bg-gray-300 px-2 rounded" onClick={refresh}>
          Odśwież
        </button>
      </div>

      <div className="flex mb-4">
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Nazwa przepisu"
          className="border p-2 rounded-l w-full"
        />
        <select
          className="border p-2"
          value={categoryId}
          onChange={e => setCategoryId(e.target.value ? Number(e.target.value) : "")}
        >
          <option value="">Kategoria...</option>
          {categories.map((cat: any) => (
            <option key={cat.id} value={cat.id}>
              {cat.name}
            </option>
          ))}
        </select>
        <button className="bg-green-500 text-white px-4 rounded-r" onClick={handleAdd}>
          Dodaj
        </button>
      </div>

      <ul>
        {filtered.map((rec: any) => (
          <li key={rec.id} className="flex items-center border-b py-2">
            <span className="font-semibold mr-2">{rec.name}</span>
            {rec.category_id && (
              <span className="bg-blue-100 text-blue-600 px-2 rounded text-xs">
                {categories.find((cat: any) => cat.id === rec.category_id)?.name}
              </span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}