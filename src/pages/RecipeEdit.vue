<script setup lang="ts">
import type { EditableRecipe, Food, Qualifier, Unit } from "@/types/recipes";
import type { User } from "@/types/users";

import { Form, useForm } from "@inertiajs/vue3";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import DescriptionItem from "@/components/DescriptionItem.vue";
import IngredientEditor from "@/components/forms/IngredientEditor.vue";
import IngredientGroupEditor from "@/components/forms/IngredientGroupEditor.vue";
import InputField from "@/components/forms/inputs/InputField.vue";
import SlugField from "@/components/forms/inputs/SlugField.vue";
import TextInput from "@/components/forms/inputs/TextInput.vue";
import StepEditor from "@/components/forms/StepEditor.vue";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{
  recipe?: EditableRecipe | null;
  qualifiers?: Qualifier[];
  foods?: Food[];
  units?: Unit[];
  user: User;
  locale: string;
}>();

const recipeForm = useForm<EditableRecipe>({
  id: props.recipe?.id || null,
  name: props.recipe?.name || "",
  slug: props.recipe?.slug || "",
  description: props.recipe?.description || "",
  prep_time: props.recipe?.prep_time || "",
  cook_time: props.recipe?.cook_time || "",
  cook_time_max: props.recipe?.cook_time_max || "",
  yield_amount: props.recipe?.yield_amount || null,
  servings: props.recipe?.servings || 1,
  ingredients: props.recipe?.ingredients || [],
  ingredient_groups: props.recipe?.ingredient_groups || [],
  steps: props.recipe?.steps || [],
});

const { t } = useI18n();
const pageTitle = computed(() =>
  props.recipe ? t("edit.title", { name: props.recipe.name }) : t("recipe.add_new"),
);

const submitRecipeForm = () => {
  recipeForm.post(`${window.location.pathname}${window.location.search}`, {
    only: ["recipe", "ingredients", "ingredientGroups"],
    preserveScroll: true,
    viewTransition: false,
  });
};
const hasErrors = computed((): boolean =>
  recipeForm.errors ? Object.keys(recipeForm.errors).length > 0 : false,
);
</script>

<template>
  <head-section :title="pageTitle" />
  <div class="container mx-auto px-4">
    <Form
      v-slot="{ errors }"
      class="grid grid-cols-12 gap-4 border-b border-t border-red-500/0"
      :class="hasErrors ? 'border-red-500' : ''"
      @submit.prevent="submitRecipeForm"
    >
      <div class="col-span-12">
        <div class="flex flex-wrap sm:flex-nowrap items-center mb-2 md:mb-4">
          <h1
            class="text-2xl pt-2 grow w-full sm:w-auto"
            itemprop="name"
            :style="recipe ? `view-transition-name: recipe-${recipe.slug}-name` : ''"
          >
            {{ pageTitle }}
          </h1>
        </div>
        <breadcrumb-bar
          :current="pageTitle"
          class="p-0"
        />
        <description-item :label="t('edit.name')">
          <input-field
            id="name-field"
            v-model="recipeForm.name"
            :errors="errors?.name"
          />
          <slug-field
            id="slug-field"
            v-model="recipeForm.slug"
            :errors="errors?.slug"
            :source-value="recipeForm.name"
            class="ml-4"
          />
        </description-item>
        <description-item :label="t('edit.yield')">
          <input-field
            id="yield-field"
            v-model="recipeForm.yield_amount"
            :errors="errors?.yield_amount"
            input-class="w-20"
            placeholder="1"
          />
        </description-item>
        <description-item :label="t('edit.servings')">
          <input-field
            id="servings-field"
            v-model="recipeForm.servings"
            :errors="errors?.servings"
            input-class="w-20"
            placeholder="1"
          />
        </description-item>
        <description-item :label="t('edit.cook_time')">
          <input-field
            id="cook-time-field"
            v-model="recipeForm.cook_time"
            placeholder="00:00:00"
            :errors="errors?.cook_time"
            input-class="w-50"
          />
        </description-item>
        <description-item :label="t('edit.prep_time')">
          <input-field
            id="prep-time-field"
            v-model="recipeForm.prep_time"
            placeholder="00:00:00"
            :errors="errors?.prep_time"
            input-class="w-50"
          />
        </description-item>
        <description-item :label="t('edit.description')">
          <text-input
            id="description-field"
            v-model="recipeForm.description"
            class="max-w-full"
            :errors="errors?.description"
            :placeholder="t('edit.description')"
          />
        </description-item>
        <div class="mt-4">
          <ingredient-group-editor
            v-model="recipeForm.ingredient_groups"
            class="mb-4"
          />
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
              </div>
            </div>
            <div class="card-body">
              <ingredient-editor
                v-model="recipeForm.ingredients"
                :errors="recipeForm.errors"
                :units="units"
                :foods="foods"
                :qualifiers="qualifiers"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-12">
        <step-editor
          v-model:steps="recipeForm.steps"
          :errors="errors"
        />
        <div class="flex justify-end">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!recipeForm.isDirty"
          >
            {{ t("edit.save") }}
          </button>
        </div>
      </div>
    </Form>
  </div>
</template>
