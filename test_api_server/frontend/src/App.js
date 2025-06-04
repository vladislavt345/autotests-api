import React, { useEffect, useState } from "react";

const styles = {
  app: {
    backgroundColor: "#121212",
    color: "#E0E0E0",
    minHeight: "100vh",
    padding: "2rem",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  title: {
    fontWeight: "300",
    fontSize: "2.5rem",
    marginBottom: "1rem",
    letterSpacing: "0.1em",
  },
  list: {
    listStyle: "none",
    padding: 0,
    width: "100%",
    maxWidth: 600,
    marginBottom: "2rem",
  },
  listItem: {
    backgroundColor: "#1E1E1E",
    marginBottom: "0.5rem",
    padding: "0.75rem 1rem",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.4)",
    fontWeight: "400",
    fontSize: "1.1rem",
  },
  subtitle: {
    fontWeight: "300",
    fontSize: "1.8rem",
    marginBottom: "1rem",
    letterSpacing: "0.07em",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
    maxWidth: 600,
  },
  input: {
    backgroundColor: "#1E1E1E",
    border: "1px solid #333",
    borderRadius: "6px",
    color: "#E0E0E0",
    padding: "0.75rem 1rem",
    marginBottom: "1rem",
    fontSize: "1rem",
    outline: "none",
    transition: "border-color 0.3s",
  },
  inputFocus: {
    borderColor: "#A67C00",
  },
  button: {
    backgroundColor: "#A67C00",
    color: "#121212",
    border: "none",
    padding: "0.85rem 1.5rem",
    fontSize: "1.1rem",
    fontWeight: "600",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "background-color 0.3s",
  },
  buttonHover: {
    backgroundColor: "#855f00",
  },
};

export default function App() {
  const [cats, setCats] = useState([]);
  const [form, setForm] = useState({ name: "", breed: "", age: "" });
  const [focusedInput, setFocusedInput] = useState(null);
  const [buttonHovered, setButtonHovered] = useState(false);

  useEffect(() => {
    fetch("/cats")
      .then((res) => res.json())
      .then(setCats);
  }, []);

  function onChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function onSubmit(e) {
    e.preventDefault();
    fetch("/cats", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...form, age: Number(form.age) }),
    })
      .then((res) => res.json())
      .then((newCat) => {
        setCats([...cats, newCat]);
        setForm({ name: "", breed: "", age: "" });
      });
  }

  return (
    <div style={styles.app}>
      <h1 style={styles.title}>Котики</h1>
      <ul style={styles.list}>
        {cats.map((cat) => (
          <li key={cat.id} style={styles.listItem}>
            {cat.name} — {cat.breed}, {cat.age} {cat.age === 1 ? "год" : "лет"}
          </li>
        ))}
      </ul>

      <h2 style={styles.subtitle}>Добавить котика</h2>
      <form style={styles.form} onSubmit={onSubmit}>
        {["name", "breed", "age"].map((field) => (
          <input
            key={field}
            name={field}
            placeholder={
              field === "name"
                ? "Имя"
                : field === "breed"
                ? "Порода"
                : "Возраст"
            }
            type={field === "age" ? "number" : "text"}
            value={form[field]}
            onChange={onChange}
            required
            min={field === "age" ? 0 : undefined}
            style={{
              ...styles.input,
              ...(focusedInput === field ? styles.inputFocus : {}),
            }}
            onFocus={() => setFocusedInput(field)}
            onBlur={() => setFocusedInput(null)}
          />
        ))}
        <button
          type="submit"
          style={{
            ...styles.button,
            ...(buttonHovered ? styles.buttonHover : {}),
          }}
          onMouseEnter={() => setButtonHovered(true)}
          onMouseLeave={() => setButtonHovered(false)}
        >
          Добавить
        </button>
      </form>
    </div>
  );
}
