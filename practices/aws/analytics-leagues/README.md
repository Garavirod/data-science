# Find port and kill process if postgres port is in used

```sh
netstat -aon | findstr :5432
taskkill/pid <el pid de la task> /F
```

# Run project in dev mod
```sh
astro dev start
```