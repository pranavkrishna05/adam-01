import { createContext, useContext, useReducer, useMemo } from "react";

/**
 * Cart Context
 * Handles cart state across the application
 */

const CartContext = createContext(undefined);

/**
 * Cart reducer
 */
const cartReducer = (state, action) => {
  switch (action.type) {
    case "ADD_TO_CART": {
      const existingItem = state.find(
        item => item.id === action.payload.id
      );

      if (existingItem) {
        return state.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }

      return [...state, { ...action.payload, quantity: 1 }];
    }

    case "INCREASE_QTY":
      return state.map(item =>
        item.id === action.payload
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );

    case "DECREASE_QTY":
      return state.map(item =>
        item.id === action.payload && item.quantity > 1
          ? { ...item, quantity: item.quantity - 1 }
          : item
      );

    case "REMOVE_FROM_CART":
      return state.filter(item => item.id !== action.payload);

    case "CLEAR_CART":
      return [];

    default:
      return state;
  }
};

/**
 * Cart Provider
 */
export const CartProvider = ({ children }) => {
  const [cart, dispatch] = useReducer(cartReducer, []);

  // Actions
  const addToCart = (product) => {
    dispatch({ type: "ADD_TO_CART", payload: product });
  };

  const increaseQty = (id) => {
    dispatch({ type: "INCREASE_QTY", payload: id });
  };

  const decreaseQty = (id) => {
    dispatch({ type: "DECREASE_QTY", payload: id });
  };

  const removeFromCart = (id) => {
    dispatch({ type: "REMOVE_FROM_CART", payload: id });
  };

  const clearCart = () => {
    dispatch({ type: "CLEAR_CART" });
  };

  const value = useMemo(
    () => ({
      cart,
      addToCart,
      increaseQty,
      decreaseQty,
      removeFromCart,
      clearCart
    }),
    [cart]
  );

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

/**
 * Custom hook
 */
export const useCart = () => {
  const context = useContext(CartContext);

  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }

  return context;
};
