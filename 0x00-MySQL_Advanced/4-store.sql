-- Script that creates a trigger that decrease a value of item after order.
CREATE TRIGGER after_order AFTER INSERT on orders FOR EACH ROW
	UPDATE items SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
