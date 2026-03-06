<script setup lang="ts">
import type {
  EditableIngredient,
  EditableRecipe,
  Food,
  IngredientGroup,
  Qualifier,
  Unit,
} from "@/types/recipes";
import type { User } from "@/types/users";

import { Deferred, useForm } from "@inertiajs/vue3";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import DescriptionItem from "@/components/DescriptionItem.vue";
import SelectInput from "@/components/SelectInput.vue";
import SortableList from "@/components/SortableList.vue";
import HeadSection from "@/layouts/HeadSection.vue";

interface FormErrors {
  name?: string[];
  description?: string[];
  servings?: string[];
  ingredients?: string[];
  ingredientGroups?: string[];
  steps?: string[];
}

const props = defineProps<{
  recipe?: EditableRecipe | null;
  ingredients?: EditableIngredient[];
  ingredientGroups?: IngredientGroup[];
  errors: FormErrors | null;
  qualifiers?: Qualifier[];
  foods?: Food[];
  units?: Unit[];
  user: User;
  locale: string;
}>();

const recipeForm = useForm({
  name: props.recipe?.name || "",
  description: props.recipe?.description || "",
  prep_time: props.recipe?.prep_time || "",
  cook_time: props.recipe?.cook_time || "",
  yield_amount: props.recipe?.yield_amount || "",
  servings: props.recipe?.servings || "",
  ingredients: props.ingredients || [],
  ingredient_groups: props.ingredientGroups || [],
  steps: props.recipe?.steps || [],
});

const { t } = useI18n();
const pageTitle = computed(() =>
  props.recipe ? t("edit.title", { name: props.recipe.name }) : t("recipe.add_new"),
);

const addIngredientGroup = () => {
  recipeForm.ingredient_groups.push({
    id: null,
    order: recipeForm.ingredient_groups.length + 1,
    name: "",
  });
};
const addIngredient = () => {
  recipeForm.ingredients.push({
    id: null,
    order: recipeForm.ingredients.length + 1,
    amount: 0,
    amount_max: null,
    food_id: null,
    unit_id: null,
    group_id: null,
    qualifier_id: null,
    optional: false,
    note: "",
  });
};
const submitRecipeForm = () => {
  recipeForm.post(`${window.location.pathname}${window.location.search}`, {
    only: ["recipe", "ingredients", "ingredientGroups"],
    preserveScroll: true,
    viewTransition: false,
  });
};
</script>

<template>
  <head-section :title="pageTitle" />
  <div class="container mx-auto px-4">
    <form
      class="grid grid-cols-12 gap-4"
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
          <input
            v-model="recipeForm.name"
            class="input"
          />
        </description-item>
        <description-item :label="t('edit.yield')">
          <input
            v-model="recipeForm.yield_amount"
            class="input w-20"
          />
        </description-item>
        <description-item :label="t('edit.servings')">
          <input
            v-model="recipeForm.servings"
            class="input w-20"
          />
        </description-item>
        <description-item :label="t('edit.cook_time')">
          <input
            v-model="recipeForm.cook_time"
            class="input w-50"
          />
        </description-item>
        <description-item :label="t('edit.prep_time')">
          <input
            v-model="recipeForm.prep_time"
            class="input w-50"
          />
        </description-item>
        <description-item :label="t('edit.description')">
          <textarea
            v-model="recipeForm.description"
            class="textarea max-w-full"
            :placeholder="t('edit.description')"
          />
        </description-item>
        <div class="mt-4">
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("edit.ingredientGroups") }}</h2>
              </div>
            </div>
            <div class="card-body">
              <div v-if="!recipeForm.ingredient_groups.length">
                {{ t("edit.no_ingredient_groups") }}
              </div>
              <sortable-list v-model="recipeForm.ingredient_groups">
                <template #default="{ item: group }">
                  <div class="flex items-center gap-2">
                    <span class="icon-[tabler--grip-vertical] cursor-move"></span>
                    <input
                      v-model="group.name"
                      class="input grow"
                    />
                  </div>
                </template>
              </sortable-list>
              <button
                type="button"
                class="btn btn-secondary mt-4"
                @click="addIngredientGroup"
              >
                {{ t("edit.add_group") }}
              </button>
            </div>
          </div>
          <div class="card p-4">
            <div class="card-title pb-2">
              <div class="flex flex-row items-center">
                <h2 class="text-xxl grow w-100 mr-2">{{ t("recipe.ingredients") }}</h2>
              </div>
            </div>
            <div class="card-body">
              <div class="flex items-center justify-between gap-2 w-full">
                <div class="w-10">{{ t("edit.order") }}</div>
                <div class="">{{ t("edit.amount") }}</div>
                <div class="">{{ t("edit.food") }}</div>
                <div class="">{{ t("edit.unit") }}</div>
                <div class="">{{ t("edit.qualifier") }}</div>
                <div class="w-12">{{ t("edit.optional") }}</div>
                <div class="">{{ t("edit.notes") }}</div>
              </div>
              <div v-if="!recipeForm.ingredients.length">
                {{ t("edit.no_ingredients") }}
              </div>
              <sortable-list v-model="recipeForm.ingredients">
                <template #default="{ item: ingredient, index: i }">
                  <div class="flex items-center gap-2 w-full">
                    <div class="flex items-center w-10 cursor-move userselect-none">
                      <span class="icon-[tabler--grip-vertical]"></span>
                    </div>
                    <div class="join">
                      <input
                        v-model="ingredient.amount"
                        class="input join-item"
                      />
                      <input
                        v-model="ingredient.amount_max"
                        class="input join-item"
                      />
                    </div>
                    <deferred data="foods">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="foods"
                        :id="`ingredient-${i}-food`"
                        v-model="ingredient.food_id"
                        :options="foods"
                        label-key="name"
                      />
                    </deferred>
                    <deferred data="units">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="units"
                        :id="`ingredient-${i}-unit`"
                        v-model="ingredient.unit_id"
                        :options="units"
                        label-key="name"
                      >
                        <template #option="{ option }">
                          {{ option.name
                          }}<template v-if="option.abbreviation"> ({{ option.abbreviation }})</template>
                        </template>
                      </select-input>
                    </deferred>
                    <deferred data="qualifiers">
                      <template #fallback>
                        <div>Loading...</div>
                      </template>
                      <select-input
                        v-if="qualifiers"
                        :id="`ingredient-${i}-qualifier`"
                        v-model="ingredient.qualifier_id"
                        :options="qualifiers"
                        label-key="title"
                      />
                    </deferred>
                    <div class="flex items-center gap-1">
                      <input
                        :id="`optional-${i}`"
                        v-model="ingredient.optional"
                        type="checkbox"
                        class="checkbox"
                      />
                      <label
                        class="sr-only"
                        :for="`optional-${i}`"
                        >{{ t("edit.optional") }}</label
                      >
                    </div>
                    <input
                      v-model="ingredient.note"
                      class="input"
                    />
                  </div>
                </template>
              </sortable-list>
              <button
                type="button"
                class="btn btn-secondary mt-4"
                @click="addIngredient"
              >
                {{ t("edit.add_ingredient") }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-12">
        <div v-if="!recipeForm.steps.length">
          {{ t("edit.no_steps") }}
        </div>
        <sortable-list v-model="recipeForm.steps">
          <template #default="{ item: step }">
            <div class="card mb-2 flex flex-row items-center cursor-move">
              <span class="ml-4 icon-[tabler--grip-vertical]"></span>
              <h3 class="card-title p-4">{{ t("recipe.step_title", { step: step.order }) }}</h3>
              <div class="card-body p-4 grow">
                <textarea
                  v-model="step.text"
                  class="textarea"
                ></textarea>
              </div>
            </div>
          </template>
        </sortable-list>
        <button
          type="button"
          class="btn btn-secondary mt-4"
        >
          {{ t("edit.add_step") }}
        </button>
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
    </form>
  </div>
</template>
