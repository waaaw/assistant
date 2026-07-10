FROM node:22-alpine AS build
WORKDIR /app
RUN corepack enable
COPY package.json .
RUN corepack pnpm install
COPY . .
RUN corepack pnpm build
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]

