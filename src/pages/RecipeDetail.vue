<script setup lang="ts">
import type { User } from "../types/users";
import type { Recipe, Ingredient } from "../types/recipes";

import { ref } from "vue";
import { router } from "@inertiajs/vue3";

import PButton from "primevue/button";
import NutritionalInformation from "../components/NutritionalInformation.vue";
import HeadSection from "../layouts/HeadSection.vue";
import { useI18n } from "vue-i18n";
import UserAvatar from "@/components/UserAvatar.vue";
import RecipeSource from "@/components/RecipeSource.vue";
import KeepAwake from "@/components/KeepAwake.vue";

interface FormErrors {
  servings?: string[];
}

const props = defineProps<{
  recipe: Recipe;
  ingredients: Ingredient[];
  servings: number;
  errors: FormErrors | null;
  user?: User;
}>();

const { t } = useI18n();

const formatDuration = (duration: string) => {
  const [h, m, s] = duration.split(":");
  return Object.entries({ h, m, s })
    .reduce((acc, [n, v]) => {
      const f = parseInt(v);
      return f ? acc + ` ${f}${n}` : acc;
    }, "")
    .trim();
};

const formatIsoDuration = (duration: string): string =>
  `PT${formatDuration(duration).replace(" ", "").toUpperCase()}`;
const servingAmount = ref<number>(props.servings || 1);
const formError = ref<string | undefined>();

const updateServings = (multiplier: number) => {
  if (!servingAmount.value) {
    servingAmount.value = props.servings;
    return;
  }
  const newValue = servingAmount.value * multiplier;
  if (newValue > 100 || newValue < 0.125) {
    formError.value = "Serving value must be between 0.125 and 100";
    servingAmount.value = props.servings;
    return;
  }
  // TODO: use `useForm` when django-inertia supports it.
  router.visit(`${window.location.pathname}?servings=${newValue}`, {
    only: ["ingredients", "servings", "errors"],
  });
};
</script>

<template>
  <HeadSection :title="recipe.name" />
  <div
    class="container mx-auto px-4"
    itemscope
    itemtype="https://schema.org/Recipe"
  >
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 sm:col-span-9 md:col-span-8">
        <div class="flex flex-wrap sm:flex-nowrap">
          <h1
            class="text-4xl mb-4 cursive flex-grow"
            itemprop="name"
          >
            {{ recipe.name }}
          </h1>
          <rating
            v-tooltip="t('recipe.ratings', recipe.num_ratings)"
            :model-value="recipe.avg_rating"
            :readonly="true"
            class="flex-grow sm:flex-grow-0"
          />
        </div>
        <div
          v-if="recipe.categories"
          class="flex align-items-center py-3"
        >
          <div class="w-1/4 text-500 font-medium">{{ t("recipe.categories") }}</div>
          <div class="w-3/4">
            <tag
              v-for="c in recipe.categories"
              :key="c.slug"
              :value="c.name"
              class="mx-1"
              severity="secondary"
            />
          </div>
        </div>
        <div class="flex align-items-center py-3">
          <div class="w-1/4 text-500 font-medium">{{ t("recipe.yields") }}</div>
          <div class="w-3/4">
            <span
              v-if="recipe.yield_unit"
              itemprop="recipeYield"
              >{{ recipe.yield_amount }} {{ recipe.yield_unit }} ({{ t('recipe.servings', servings) }})</span
            >
            <span v-else>{{ t('recipe.servings', servings) }}</span>
          </div>
        </div>
        <div class="flex align-items-center py-3">
          <div class="w-1/4 text-500 font-medium">{{ t("recipe.added_by") }}</div>
          <div class="w-3/4 flex items-center">
            <UserAvatar :user="recipe.added_by" size="normal" />
            <span class="pl-2">{{
              recipe.added_by.id === user?.id ? t("users.me") : recipe.added_by.full_name
            }}</span>
          </div>
        </div>
        <div
          v-if="recipe.source"
          class="flex align-items-center py-3"
        >
          <div class="w-1/4 text-500 font-medium">{{ t("recipe.from") }}</div>
          <div class="w-3/4">
            <recipe-source :source="recipe.source" :value="recipe.source_value" />
          </div>
        </div>
        <divider v-if="recipe.description" />
        <div
          class="mt-2 pb-5"
          itemprop="description"
        >
          {{ recipe.description }}
        </div>
        <splitter
          v-if="recipe.total_time"
          class="mb-5"
        >
          <splitter-panel
            v-if="recipe.prep_time"
            class="flex items-center justify-center m-2"
          >
            {{ t("times.prep") }}&nbsp;<meta
              itemprop="prepTime"
              :content="formatIsoDuration(recipe.prep_time)"
            />{{ formatDuration(recipe.prep_time) }}
          </splitter-panel>
          <splitter-panel
            v-if="recipe.cook_time"
            class="flex items-center justify-center m-2"
          >
            {{ t("times.cook") }}&nbsp;<meta
              itemprop="prepTime"
              :content="formatIsoDuration(recipe.cook_time)"
            />{{ formatDuration(recipe.cook_time) }}
          </splitter-panel>
          <splitter-panel
            v-if="recipe.total_time"
            class="flex items-center justify-center m-2"
          >
            {{ t("times.total") }}&nbsp;<meta
              itemprop="prepTime"
              :content="formatIsoDuration(recipe.total_time)"
            />{{ formatDuration(recipe.total_time) }}
          </splitter-panel>
        </splitter>
        <div class="ingredients">
          <card>
            <template #title>
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
                <div class="grow-0">
                  <input-group class="grow-0">
                    <PButton
                      :disabled="!servingAmount || servingAmount / 2 <= 0.125"
                      @click="updateServings(0.5)"
                      >½</PButton
                    >
                    <input-number
                      v-model="servingAmount"
                      placeholder="servings"
                      :min="0.125"
                      :max="100"
                      input-class="text-center pa-0"
                      :fluid="true"
                      @update="updateServings(1)"
                    />
                    <PButton
                      :disabled="servingAmount * 2 >= 100"
                      @click="updateServings(2)"
                      >x2</PButton
                    >
                  </input-group>
                  <p
                    v-if="errors?.servings?.length"
                    class="text-xs text-red-600"
                  >
                    {{ errors.servings[0] }}
                  </p>
                </div>
              </div>
            </template>
            <template #content>
              <ul>
                <li
                  v-for="ingredient in ingredients"
                  :key="ingredient.id"
                >
                  <i18n-t
                    keypath="recipe.ingredient"
                    tag="span"
                  >
                    <template #amount>{{ ingredient.amount_display }}</template>
                    <template #ingredient>
                      <strong>{{ ingredient.food_display }}</strong>
                    </template>
                  </i18n-t>
                  <span
                    v-if="ingredient.qualifier"
                    class="qualifier"
                    >, {{ ingredient.qualifier }}</span
                  >
                  <span
                    v-if="ingredient.optional"
                    class="optional"
                    >*Optional</span
                  >
                  <span v-if="ingredient.note">&nbsp;({{ ingredient.note }})</span>
                </li>
              </ul>
            </template>
          </card>
        </div>
      </div>
      <div class="col-span-12 sm:col-span-3 md:col-span-4">
        <div
          v-if="recipe.thumbnail_image_url"
          class="overflow-clip p-card"
        >
          <img
            :src="recipe.thumbnail_image_url"
            :alt="recipe.name"
            class="w-full"
          />
        </div>
        <NutritionalInformation
          v-if="recipe.nutrition"
          :nutrition="recipe.nutrition"
          :servings="servings"
          class="mt-4"
        />
      </div>
      <div class="col-span-12 md:col-span-8">
        <div class="flex flex-row">
          <h2 class="text-xl mb-2 flex-grow">{{ t("recipe.directions") }}</h2>
          <KeepAwake />
        </div>
        <Panel
          v-for="(step, i) in recipe.steps"
          :key="i"
          toggleable
          class="mb-2"
          :header="t('recipe.step_title', { step: i + 1})"
          itemprop="recipeInstructions"
        >
          {{ step }}
        </Panel>
      </div>
    </div>
  </div>
</template>
