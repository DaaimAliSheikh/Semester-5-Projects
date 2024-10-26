'use client'
import React, { useEffect, useState } from 'react';
import { TextField, Button, Typography, Box, Paper, List, ListItem, ListItemText } from '@mui/material';
import axios from 'axios';
import { serverURL } from '@/serverURL';
import { BookI } from '@/types';




function BookForm() {
  const [Author, setAuthor] = useState('');
  const [Title, setTitle] = useState('');
  const [books, setBooks] = useState<BookI[]>([]);

  const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
        const response = await axios.post(serverURL +'/books', { Author, Title })
        const submittedBook: BookI = response.data;
        setBooks([...books, submittedBook]);
        setAuthor('');
        setTitle('');
    }
    catch (error) {
        console.error('Error submitting book');
      }
  };

  useEffect(() => {
    // Fetch books when the component mounts
    const fetchBooks = async () => {
      try {
        const response = await axios.get(serverURL +'/books')
        const books: BookI[] =  response.data;
        setBooks(books);
      } catch (error) {
        console.error('Error fetching books');
      }
    };

    fetchBooks();
  }, []);

  return (
    <Box sx={{ maxWidth: 400, margin: 'auto', mt: 5 }}>
      <Typography variant="h5" gutterBottom>
        Add a New Book
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Author"
          variant="outlined"
          fullWidth
          margin="normal"
          value={Author}
          onChange={(e) => setAuthor(e.target.value)}
          required
        />
        <TextField
          label="Title"
          variant="outlined"
          fullWidth
          margin="normal"
          value={Title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
          Submit
        </Button>
      </form>
      {books.length > 0 && (
        <Paper elevation={3} sx={{ mt: 4, p: 2 }}>
          <Typography variant="h6" gutterBottom>All Books</Typography>
          <List>
            {books.map((book, index) => (
              <>
              <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
              <Typography variant="h5">{`Title: ${book.Title}`}</Typography>
              <Typography variant="subtitle1">{`Author: ${book.Author}`}</Typography>
              <Typography variant="subtitle2">{`ISBN_NO: ${book.ISBN_NO}`}</Typography>
              </ListItem>
              </>
            
               
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
}

export default BookForm;
