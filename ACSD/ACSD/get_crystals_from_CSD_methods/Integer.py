class Integer:
    def __init__(self, value):
        """
        Constructor for Integer class.

        Parameters:
            value (int): The initial integer value for this Integer object.

        Raises:
            TypeError: If `value` is not of type int.
        """
        if isinstance(value, int):
            self.value = value
        else:
            raise TypeError("Integer class only supports integer values")

    def __repr__(self):
        """
        Returns a string representation of the Integer object.

        Returns:
            str: The string representation of the Integer object.
        """
        return f'Integer({self.value})'

    def __str__(self):
        """
        Returns a string representation of the Integer object.

        Returns:
            str: The string representation of the Integer object.
        """
        return str(self.value)

    def __add__(self, other):
        """
        Adds this Integer object with another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to add.

        Returns:
            Integer: A new Integer object representing the sum.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        elif isinstance(other, int):
            return Integer(self.value + other)
        else:
            raise TypeError("Unsupported operand types for +: Integer and " + type(other).__name__)

    def __iadd__(self, other):
        """
        Performs in-place addition (+=) with this Integer object and another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to add in-place.

        Returns:
            Integer: The updated Integer object after in-place addition.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            self.value += other.value
        elif isinstance(other, int):
            self.value += other
        else:
            raise TypeError("Unsupported operand types for +=: Integer and " + type(other).__name__)
        return self

    def __sub__(self, other):
        """
        Subtracts another Integer object or int from this Integer object.

        Parameters:
            other (Integer or int): The Integer object or int to subtract.

        Returns:
            Integer: A new Integer object representing the difference.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            return Integer(self.value - other.value)
        elif isinstance(other, int):
            return Integer(self.value - other)
        else:
            raise TypeError("Unsupported operand types for -: Integer and " + type(other).__name__)

    def __isub__(self, other):
        """
        Performs in-place subtraction (-=) with this Integer object and another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to subtract in-place.

        Returns:
            Integer: The updated Integer object after in-place subtraction.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            self.value -= other.value
        elif isinstance(other, int):
            self.value -= other
        else:
            raise TypeError("Unsupported operand types for -=: Integer and " + type(other).__name__)
        return self

    def __mul__(self, other):
        """
        Multiplies this Integer object with another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to multiply.

        Returns:
            Integer: A new Integer object representing the product.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, int):
            return Integer(self.value * other)
        else:
            raise TypeError("Unsupported operand types for *: Integer and " + type(other).__name__)

    def __imul__(self, other):
        """
        Performs in-place multiplication (*=) with this Integer object and another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to multiply in-place.

        Returns:
            Integer: The updated Integer object after in-place multiplication.
        
        Raises:
            TypeError: If `other` is not an Integer or int.
        """
        if isinstance(other, Integer):
            self.value *= other.value
        elif isinstance(other, int):
            self.value *= other
        else:
            raise TypeError("Unsupported operand types for *=: Integer and " + type(other).__name__)
        return self

    def __eq__(self, other):
        """
        Checks if this Integer object is equal to another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        if isinstance(other, Integer):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return NotImplemented

    def __lt__(self, other):
        """
        Checks if this Integer object is less than another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to compare.

        Returns:
            bool: True if less than, False otherwise.
        """
        if isinstance(other, Integer):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        Checks if this Integer object is greater than another Integer object or int.

        Parameters:
            other (Integer or int): The Integer object or int to compare.

        Returns:
            bool: True if greater than, False otherwise.
        """
        if isinstance(other, Integer):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        else:
            return NotImplemented
